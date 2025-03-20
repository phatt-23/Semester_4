import xml.etree.ElementTree as ET
INPUT_XML = '<class class_id="SKJ-2021S"><student student_id="ABC0123"><task task_id="1">4</task><task task_id="2">4</task><task task_id="3">4</task><task task_id="4">0</task><task task_id="5">4</task><task task_id="6">5</task><task task_id="7">5</task><task task_id="8">0</task></student><student student_id="DEF4567"><task task_id="1">4</task><task task_id="2">4</task><task task_id="3">4</task><task task_id="4">4</task><task task_id="5">3</task><task task_id="6">2</task><task task_id="7">1</task><task task_id="8">1</task></student><student student_id="GHI8901"><task task_id="1">1</task><task task_id="2">2</task><task task_id="3">3</task><task task_id="4">2</task><task task_id="5">3</task><task task_id="6">4</task><task task_id="7">4</task><task task_id="8">4</task></student><student student_id="JKL2345"><task task_id="1">4</task><task task_id="2">1</task><task task_id="3">2</task><task task_id="4">5</task><task task_id="5">0</task><task task_id="6">5</task><task task_id="7">5</task><task task_id="8">4</task></student><student student_id="MNO6789"><task task_id="1">2</task><task task_id="2">1</task><task task_id="3">4</task><task task_id="4">0</task><task task_id="5">2</task><task task_id="6">5</task><task task_id="7">2</task><task task_id="8">2</task></student><student student_id="PQR0123"><task task_id="1">0</task><task task_id="2">2</task><task task_id="3">2</task><task task_id="4">3</task><task task_id="5">1</task><task task_id="6">4</task><task task_id="7">1</task><task task_id="8">5</task></student></class>'


def create_student(xml_root: ET.Element, student_id: str):
    '''
    Vytvořte studenta dle loginu.
    Ujistěte se, že student neexistuje, jinak: raise Exception('student already exists')
    '''

    for student in xml_root.findall("student"):
        if student_id == student.get("student_id"):
            raise Exception("student already exists")

    xml_root.append(ET.Element("student", student_id=student_id))



def remove_student(xml_root: ET.Element, student_id: str):
    '''
    Odstraňte studenta dle loginu
    '''
    for student in xml_root.findall("student"):
        if student_id == student.get("student_id"):
            xml_root.remove(student)


def set_task_points(xml_root: ET.Element, student_id: str, task_id: str, points: str):
    '''
    Přepište body danému studentovi u jednoho tasku
    '''
    student = xml_root.find(f"student[@student_id='{student_id}']")
    # print("student:", student)
    if student is None:
        return

    task = student.find(f"task[@task_id='{task_id}']")
    # print("task:", task)
    if task is None:
        return

    task.text = points


root = ET.fromstring(INPUT_XML)
set_task_points(root, 'ABC0123', '1', '5')





def create_task(xml_root: ET.Element, student_id: str, task_id: str, points: str):
    '''
    Pro daného studenta vytvořte task s body.
    Ujistěte se, že task (s task_id) u studenta neexistuje, jinak: raise Exception('task already exists')
    '''
    student = xml_root.find(f"student[@student_id='{student_id}']")
    if student is None:
        return

    if student.find(f"task[@task_id='{task_id}']") is not None:
        raise Exception("task already exists")

    new_task = ET.Element("task", attrib={ "task_id": task_id })
    new_task.text = points
    student.append(new_task)




def remove_task(xml_root: ET.Element, task_id: str):
    '''
    Napříč všemi studenty smažte task s daným task_id
    '''
    for student in xml_root.findall("student"):
        task = student.find(f"task[@task_id='{task_id}']")
        if task is not None:
            student.remove(task)


