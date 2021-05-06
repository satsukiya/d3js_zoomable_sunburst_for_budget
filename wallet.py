import pandas as pd
import json
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('excel_file', help='[input]予算書.xls')
    parser.add_argument('--output_file', default='output.json')    
    args = parser.parse_args()

    file_name = args.excel_file
    sheet_name = "一般会計 予定経費要求書（科目別内訳）"
    output_file = "output.json"
    dst = {}

    df = pd.read_excel(file_name,sheet_name=sheet_name)
    df = df.rename(columns={df.columns[9]: '大項目'})
    df = df.rename(columns={df.columns[10]: '小項目'})
    square = df.iloc[:, [0,1,9,10,11]]

    cols = list(square.columns[:-1])

    auth = square[square["所管"].notnull()]

    dst["name"] = "歳出"
    dst["children"] = compose_category(square, square.index.start, square.index.stop, cols)

    #end_index = ext_fields.index.stop
    #big_cat = ext_fields[ext_fields.iloc[:, 2].notnull()]

    #items = []
    #indexs = list(big_cat.index)
    #for i, idx in enumerate(indexs):
    #    _dst = {}
    #    if i == big_cat.index.size - 1:
    #        out = square[indexs[i]+1:end_index]
    #    else :
    #        out = square[indexs[i]+1:indexs[i+1]]
    #    name_value(_dst, square.iloc[idx, 2], out)
    #    items.append(_dst)
    #dst["name"] = "衆議院"
    #dst["children"] = items

    with open(args.output_file, "w") as fout:
        json.dump(dst, fout, indent=2, ensure_ascii=False)


def compose_category(data_lake, begin_index, end_index, cols, cols_index=0):
    raw_src = data_lake[begin_index:end_index]
    src = raw_src[raw_src[cols[cols_index]].notnull()]
    indexs = list(src.index)

    dst = []
    for i, idx in enumerate(indexs):
        _dst = {}
        _data = None
        _begin = indexs[i]
        _end = 0

        if i == src.index.size - 1:
            _end = end_index
        else :
            _end = indexs[i+1]

        #print("{}:{}".format(_begin, _end))
        _dst["name"] = data_lake[cols[cols_index]].iloc[indexs[i]]

        if cols_index == len(cols) - 1:
            _dst["value"] = int(data_lake["令和3年度要求額(千円)"].iloc[indexs[i]])
        else :
            _dst["children"] = compose_category(data_lake, _begin, _end, cols, cols_index + 1)
        out = data_lake[_begin:_end]
        dst.append(_dst)
    return dst


if __name__ == '__main__':
    main()