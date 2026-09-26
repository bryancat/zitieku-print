#!/usr/bin/env python3
"""离线生成与字帖库网站兼容的规范字帖链接。"""
import argparse
import base64
from copy import deepcopy
import json
from pathlib import Path
import sys
import zlib

CONTRACT = json.loads((Path(__file__).resolve().parents[1] / 'references/contract-v2.json').read_text(encoding='utf-8'))

ERROR_MESSAGES = {
    'INVALID_INPUT': '输入必须是一个 JSON 对象。',
    'INVALID_JSON': '输入不是有效的 JSON。',
    'INPUT_READ_FAILED': '无法读取输入文件。',
    'INPUT_TOO_LONG': '输入内容过长。',
    'UNKNOWN_FIELD': '输入包含当前版本不支持的字段。',
    'UNKNOWN_TEMPLATE': '找不到这个字帖方案，请先查看可用方案。',
    'MISSING_NAME': '姓名练字需要填写 student_name。',
    'NAME_TOO_LONG': '姓名最多支持 6 个字符。',
    'MISSING_CONTENT': '这个字帖方案需要填写非空的 text。',
    'INCOMPATIBLE_CONTENT': '当前方案不能同时使用这些内容字段。',
    'INVALID_CLASS': 'student_class 必须是字符串。',
    'INVALID_STUDENT_ID': 'student_id 必须是字符串。',
    'INVALID_TITLE': 'title 必须是字符串。',
    'INVALID_GRID': 'grid_type 仅支持 mi、tian 或 square。',
    'UNSUPPORTED_COLUMNS': '当前字帖方案不支持调整每行格数。',
    'INVALID_COLUMNS': 'columns 必须是 4 到 16 的整数。',
    'INVALID_ORIENTATION': '当前字帖方案不支持这个页面方向。',
    'INVALID_PINYIN': '当前字帖方案不支持这个拼音设置。',
    'INVALID_TRACE_STYLE': '当前字帖方案不支持这个描红形态。',
    'INVALID_TRACE_DENSITY': '当前字帖方案不支持这个描红浓度。',
    'INVALID_PRACTICE_GRADIENT': '当前字帖方案不支持这个练习梯度。',
    'INVALID_SOURCE': 'source 不是允许的来源标识。',
    'CONTENT_TOO_LONG': '字帖配置内容过长，无法生成链接。',
    'LINK_TOO_LONG': '生成后的字帖链接过长，请减少内容后重试。',
}

class SkillInputError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(ERROR_MESSAGES.get(code, '输入不符合当前字帖规则。'))

def fail(code):
    raise SkillInputError(code)

def compact_document(document):
    c, e, a, l, g, s, h, f = (document[key] for key in ('content','exercise','annotations','layout','grid','style','header','footer'))
    return [document['version'],
        [c['kind'],c['text'],c['title'],c['studentName'],c['studentClass'],c['studentId'],c['foundationPattern']],
        [e['kind'],[[stage['role'],stage['count']] for stage in e['stages']],e['traceStyle'],e['traceDensity']],
        [a['pinyin'],a['strokeCount'],a['radical'],a['structure']],
        [l['paper'],l['orientation'],l['flow'],l['columnDirection'],l['columns'],l['overflow'],l['poetryLayout']],
        [g['type'],g['color']],[s['fontId'],s['masterColor'],s['traceColor']],
        [h['enabled'],h['fields'],h['showStars']],[f['reprint'],f['tip']]]

def encode_document(document):
    printable = deepcopy(document)
    fields = set(printable['header']['fields']) if printable['header']['enabled'] else set()
    if 'class' not in fields: printable['content']['studentClass'] = ''
    if 'studentId' not in fields: printable['content']['studentId'] = ''
    if not printable['header']['enabled']: printable['header']['fields'] = []
    json_text = json.dumps(compact_document(printable), ensure_ascii=False, separators=(',', ':'))
    if len(json_text) > 20000: fail('CONTENT_TOO_LONG')
    raw = json_text.encode()
    compressor = zlib.compressobj(level=9, wbits=-15)
    token = '3.' + base64.urlsafe_b64encode(compressor.compress(raw) + compressor.flush()).decode().rstrip('=')
    if len(token) > CONTRACT['limits']['tokenCharacters']: fail('LINK_TOO_LONG')
    return token

def create_link(request):
    if not isinstance(request, dict): fail('INVALID_INPUT')
    if set(request) - set(CONTRACT['fields']): fail('UNKNOWN_FIELD')
    preset = next((item for item in CONTRACT['presets'] if item['id'] == request.get('template_id')), None)
    if preset is None: fail('UNKNOWN_TEMPLATE')
    document = deepcopy(preset['document'])
    content = document['content']; layout = document['layout']; exercise = document['exercise']
    controls = set(preset['capabilities']['controls']); kind = content['kind']
    if kind == 'name':
        name = request.get('student_name')
        if not isinstance(name, str) or not name.strip(): fail('MISSING_NAME')
        if len(name.strip()) > CONTRACT['limits']['nameCharacters']: fail('NAME_TOO_LONG')
        if 'text' in request: fail('INCOMPATIBLE_CONTENT')
        content['studentName'] = name.strip()
        content['studentClass'] = request.get('student_class','') if isinstance(request.get('student_class',''),str) else fail('INVALID_CLASS')
        content['studentId'] = request.get('student_id','') if isinstance(request.get('student_id',''),str) else fail('INVALID_STUDENT_ID')
    elif kind != 'foundations':
        text = request.get('text')
        if not isinstance(text,str) or not text.strip(): fail('MISSING_CONTENT')
        if 'student_name' in request: fail('INCOMPATIBLE_CONTENT')
        content['text'] = text
    elif 'text' in request or 'student_name' in request: fail('INCOMPATIBLE_CONTENT')
    if 'title' in request:
        if not isinstance(request['title'],str): fail('INVALID_TITLE')
        content['title'] = request['title']
    if 'grid_type' in request:
        if request['grid_type'] not in ('mi','tian','square'): fail('INVALID_GRID')
        document['grid']['type'] = request['grid_type']
    if 'columns' in request:
        value=request['columns']
        if 'columns' not in controls: fail('UNSUPPORTED_COLUMNS')
        if type(value) is not int or not 4 <= value <= 16: fail('INVALID_COLUMNS')
        layout['columns']=value
    if 'orientation' in request:
        value=request['orientation']
        if value not in ('portrait','landscape') or (kind=='name' and value!='portrait'): fail('INVALID_ORIENTATION')
        layout['orientation']=value
    if 'pinyin' in request:
        if 'pinyin' not in controls or type(request['pinyin']) is not bool: fail('INVALID_PINYIN')
        document['annotations']['pinyin']='tone' if request['pinyin'] else 'off'
    if 'trace_style' in request:
        if 'traceStyle' not in controls or request['trace_style'] not in ('solid','hollow'): fail('INVALID_TRACE_STYLE')
        exercise['traceStyle']=request['trace_style']
    if 'trace_density' in request:
        value=request['trace_density']
        if 'traceDensity' not in controls or value not in ('light','normal','dark'): fail('INVALID_TRACE_DENSITY')
        exercise['traceDensity']=value;document['style']['traceColor']={'light':'#d1d5db','normal':'#b8b8b8','dark':'#9ca3af'}[value]
    if 'practice_gradient' in request:
        value=request['practice_gradient']
        if 'practiceGradient' not in controls or value not in ('classic','half','all-trace'): fail('INVALID_PRACTICE_GRADIENT')
        exercise['stages'] = ([{'role':'master','count':1},{'role':'trace','count':2},{'role':'copy','count':'fill'}] if value=='classic' else
            [{'role':'master','count':1},{'role':'trace','count':max(1,layout['columns']//2-1)},{'role':'copy','count':'fill'}] if value=='half' else
            [{'role':'master','count':1},{'role':'trace','count':'fill'}])
    document['footer']['reprint']=False
    source=request.get('source','skill')
    if source not in CONTRACT['sources']: fail('INVALID_SOURCE')
    token=encode_document(document)
    return {'status':'configuration_ready','schema_version':'3','template_id':preset['id'],'template_name':preset['name'],
        'url':f'https://zitieku.com/zitie-shengchengqi.html?from={source}#reprint={token}',
        'content_length':len(content['studentName'] if kind=='name' else content['text']),'render_verified':False,
        'settings':{'grid_type':document['grid']['type'],'columns':layout['columns'],'orientation':layout['orientation']},
        'warnings':['请在网站预览中检查页面容量、字形、拼音和笔顺数据，再下载或打印。']}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', help='UTF-8 JSON 输入文件；省略时从标准输入读取')
    parser.add_argument('--list-templates', action='store_true', help='列出当前可用字帖方案')
    args=parser.parse_args()
    try:
        if args.list_templates:
            result=[{'id':p['id'],'mode':p['document']['content']['kind'],'name':p['name'],'description':p['description']} for p in CONTRACT['presets']]
        else:
            raw=Path(args.input).read_text(encoding='utf-8') if args.input else sys.stdin.read(100001)
            if len(raw)>100000: fail('INPUT_TOO_LONG')
            result=create_link(json.loads(raw))
        print(json.dumps(result,ensure_ascii=False));return 0
    except SkillInputError as error:
        print(json.dumps({'status':'error','error_code':error.code,'message':str(error)},ensure_ascii=False));return 1
    except json.JSONDecodeError:
        error=SkillInputError('INVALID_JSON')
        print(json.dumps({'status':'error','error_code':error.code,'message':str(error)},ensure_ascii=False));return 1
    except OSError:
        error=SkillInputError('INPUT_READ_FAILED')
        print(json.dumps({'status':'error','error_code':error.code,'message':str(error)},ensure_ascii=False));return 1
    except (ValueError,TypeError):
        error=SkillInputError('INVALID_INPUT')
        print(json.dumps({'status':'error','error_code':error.code,'message':str(error)},ensure_ascii=False));return 1

if __name__=='__main__': sys.exit(main())
