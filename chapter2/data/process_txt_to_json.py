import json


def process(input_file_path, output_file_path):
    data = []
    with open(input_file_path, encoding='utf-8') as fin:
        is_first_line = True
        for line in fin:
            if is_first_line:
                is_first_line = False
                continue
            line = line[:-1]  # \n
            student_number, name, height = line.split("\t")
            data.append({"student_number": student_number, "name": name, "height": height})
    result = {}
    result['data'] = data
    with open(output_file_path, mode='w', encoding='utf-8') as fout:
        fout.write(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    input_file_path = "student_information.txt"
    output_file_path = "student_information.json"
    process(input_file_path=input_file_path, output_file_path=output_file_path)
