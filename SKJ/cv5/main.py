import xml.etree.ElementTree as ET

def create_student(xml_root: ET.Element, student_id: int):
    '''
    Vytvořte studenta dle loginu.
    Ujistěte se, že student neexistuje, jinak: raise Exception('student already exists')
    '''

    for student in xml_root.findall('student'):
        if student.get('student_id') == student_id:
            raise Exception('student already exists')
    
    new_student = ET.SubElement(xml_root, 'student', student_id=str(student_id))
    return new_student


def remove_student(xml_root: ET.Element, student_id: int):
    '''
    Odstraňte studenta dle loginu
    '''

    for student in xml_root.findall('student'):
        if student.get('student_id') == str(student_id):
            xml_root.remove(student)
            return

    raise Exception('student not found')



def set_task_points(xml_root: ET.Element, student_id: int, task_id: int, points: int):
    '''
    Přepište body danému studentovi u jednoho tasku
    '''

    student = xml_root.find(f"./student[@student_id='{student_id}']")
    if student is None:
        raise Exception('student not found')
    
    task = student.find(f"task[@task_id='{task_id}']")
    if task is None:
        raise Exception('task not found')
    
    task.text = str(points)


def create_task(xml_root: ET.Element, student_id: int, task_id: int, points: int):
    '''
    Pro daného studenta vytvořte task s body.
    Ujistěte se, že task (s task_id) u studenta neexistuje, jinak: raise Exception('task already exists')
    '''

    student = xml_root.find(f"./student[@student_id='{student_id}']")
    if student is None:
        raise Exception('student not found')
    
    for task in student.findall('task'):
        if task.get('task_id') == task_id:
            raise Exception('task already exists')
    
    new_task = ET.SubElement(student, 'task', task_id=str(task_id))
    new_task.text = str(points)
    return new_task


def remove_task(xml_root: ET.Element, task_id: int):
    '''
    Napříč všemi studenty smažte task s daným task_id
    '''

    for student in xml_root.findall('student'):
        task = student.find(f"task[@task_id='{task_id}']")
        if task:
            student.remove(task)


