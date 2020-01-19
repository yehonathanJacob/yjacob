import os
import yaml
import pytest
import pytest_dependency
import glob
from collections import defaultdict
from pytest_dependency import depends

files_to_check = glob.glob("*.yaml")

exercises_valid_details = ['ranks', 'repeats', 'durations', 'two_sides', 'closed_eyes', 'weights_required']
boolean_in_details = ['weights_required', 'two_sides', 'closed_eyes']
exercises_names = ["jumping_jack", "jump", "jump_high_knees", "squat", "deep_squat", "lunges", "balance",
                   "balance_eyes_closed", "leg_to_side", "leg_to_side_eyes_closed", "stretch", "ankle_to_toe",
                   "hands_up", "hands_down", "hands_out"]


def get_dataFile(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as yaml_file:
        training_program_settings = yaml.load(yaml_file)
    return {'data': training_program_settings, 'file_name': file_name}


@pytest.fixture(scope="module", name="fileName", params=files_to_check)
def fileName(request):
    file_name = request.param
    return file_name


@pytest.fixture(scope="module", name="dataFile")
def dataFile(request, fileName):
    depends(request, ["test_syntax_and_structure[{}]".format(fileName)])
    return get_dataFile(fileName)


@pytest.mark.dependency()
@pytest.mark.xfail(reason="deliberate fail")
def test_syntax_and_structure(fileName):
    dataFile = get_dataFile(fileName)
    data, file_name = dataFile['data'], dataFile['file_name']
    assert 'work_flow' in data, f"file_name: {file_name}"
    assert 'number_of_sets' in data['work_flow'], f"file_name: {file_name}"
    assert 'exercises_per_set' in data['work_flow'], f"file_name: {file_name}"
    assert 'groups_flow' in data['work_flow'], f"file_name: {file_name}"
    assert 'flow_duration' in data['work_flow'], f"file_name: {file_name}"
    assert 'groups' in data['work_flow'], f"file_name: {file_name}"
    assert 'categories' in data['work_flow'], f"file_name: {file_name}"
    assert 'exercises' in data, f"file_name: {file_name}"


@pytest.mark.dependency()
def test_exercises_details_propriety(dataFile):
    data, file_name = dataFile['data'], dataFile['file_name']
    for exercise_name, exercise_data in data['exercises'].items():
        for detail in exercise_data:
            assert detail in exercises_valid_details, \
                f"file_name: {file_name}, exercise: {exercise_name}, detail: {detail}"


@pytest.mark.dependency()
def test_lengh_of_details_equal(dataFile):
    data, file_name = dataFile['data'], dataFile['file_name']
    for exercise_name, exercise_data in data['exercises'].items():
        assert 'ranks' in exercise_data, f"file_name: {file_name}, exercise: {exercise_name}"
        ranks_len = len(exercise_data['ranks'])
        for detail in exercise_data:
            if type(exercise_data[detail]) == list:
                assert len(exercise_data[detail]) == ranks_len, \
                    f"file_name: {file_name}, exercise: {exercise_name}, detail: {detail}, ranks_len: {ranks_len}"


@pytest.mark.dependency()
def test_boolean_in_details(dataFile):
    data, file_name = dataFile['data'], dataFile['file_name']
    for exercise_name, exercise_data in data['exercises'].items():
        for detail in exercise_data:
            if detail in boolean_in_details:
                assert type(exercise_data[detail]) == bool, \
                    f"file_name: {file_name}, exercise: {exercise_name}, detail: {detail}, type: {type(detail)}"
            else:
                assert type(exercise_data[detail]) != bool, \
                    f"file_name: {file_name}, exercise: {exercise_name}, detail: {detail}, type: {type(detail)}"


@pytest.mark.dependency()
def test_exercises_in_categories(dataFile):
    data, file_name = dataFile['data'], dataFile['file_name']
    exe_to_cat = defaultdict(list)
    for category in data['work_flow']['categories']:
        for exe in data['work_flow']['categories'][category]:
            exe_to_cat[exe].append(category)
            assert exe in exercises_names, f"file_name: {file_name}, exercise: {exe} dose not in exercises_names"
    for exe, categori_list in exe_to_cat.items():
        assert len(categori_list) == 1, f"file_name: {file_name}, exercise: {exe}, categories: {categori_list}"


@pytest.mark.dependency()
def test_exercises_in_groups_and_exercises_details(dataFile):
    data, file_name = dataFile['data'], dataFile['file_name']
    categories_exercises = []
    for category in data['work_flow']['categories']:
        categories_exercises.extend(data['work_flow']['categories'][category])
    for exe_name in data['exercises']:
        assert exe_name in categories_exercises, f"file_name: {file_name}, exercise: {exe_name}, dose not in categories"
    for group in data['work_flow']['groups']:
        for exe_name in data['work_flow']['groups'][group]:
            assert exe_name in categories_exercises, f"file_name: {file_name}, exercise: {exe_name}, dose not in categories"


@pytest.mark.dependency()
def test_groups_flow_validate(dataFile):
    data, file_name = dataFile['data'], dataFile['file_name']
    for group in data['work_flow']['groups_flow']:
        assert group in data['work_flow']['groups'], f"file_name: {file_name}, group: {group}, not in work_flow groups"


@pytest.mark.dependency()
def test_groups_flow_len(dataFile):
    data, file_name = dataFile['data'], dataFile['file_name']
    len_groups_flow = len(data['work_flow']['groups_flow'])
    exercises_per_set = data['work_flow']['exercises_per_set']
    number_of_sets = data['work_flow']['number_of_sets']
    assert len_groups_flow == exercises_per_set * number_of_sets, \
        f"file_name: {file_name}, len of groups_flow: {len_groups_flow}," \
        f" exercises_per_set: {exercises_per_set}, number_of_sets: {number_of_sets}"


if __name__ == "__main__":
    file_name = "coach_assessments.yaml"

    with open(os.path.join(os.path.dirname(__file__), os.path.join("auto_learning", file_name))) as yaml_file:
        training_program_settings = yaml.load(yaml_file)
    flow_categories = training_program_settings["work_flow"]["exercises_groups_flow"]
    flow_leftover_time = training_program_settings["work_flow"]["flow_duration"]
