import dearpygui.dearpygui as dpg
import math
from tkinter import Tk
from tkinter.filedialog import askopenfilename

easing_list = ["linear", "easeInSin", "easeOutSin", "easeInQuad", "easeOutQuad", "easeInCubic", "easeOutCubic",
               "easeInQuart", "easeOutQuart", "easeInQuint", "easeOutQuint", "easeInExpo", "easeOutExpo",
               "easeInCirc", "easeOutCirc"]

# not adding inout easings blame satte
def linear(t):
    return t

def easeInSine(t):
    return -math.cos(t * math.pi / 2) + 1

def easeOutSine(t):
    return math.sin(t * math.pi / 2)

def easeInQuad(t):
    return t * t

def easeOutQuad(t):
    return -t * (t - 2)

def easeInCubic(t):
    return t * t * t

def easeOutCubic(t):
    t -= 1
    return t * t * t + 1

def easeInQuart(t):
    return t * t * t * t

def easeOutQuart(t):
    t -= 1
    return -(t * t * t * t - 1)

def easeInQuint(t):
    return t * t * t * t * t

def easeOutQuint(t):
    t -= 1
    return t * t * t * t * t + 1

def easeInExpo(t):
    return math.pow(2, 10 * (t - 1))

def easeOutExpo(t):
    return -math.pow(2, -10 * t) + 1

def easeInCirc(t):
    if t*t >= 1:
        return 1
    return 1 - math.sqrt(1 - t * t)

def easeOutCirc(t):
    t -= 1
    return math.sqrt(1 - t * t)

def pick_easing(easing_name:str):
    if easing_name == easing_list[0]:
        return linear
    elif easing_name == easing_list[1]:
        return easeInSine
    elif easing_name == easing_list[2]:
        return easeOutSine
    elif easing_name == easing_list[3]:
        return easeInQuad
    elif easing_name == easing_list[4]:
        return easeOutQuad
    elif easing_name == easing_list[5]:
        return easeInCubic
    elif easing_name == easing_list[6]:
        return easeOutCubic
    elif easing_name == easing_list[7]:
        return easeInQuart
    elif easing_name == easing_list[8]:
        return easeOutQuart
    elif easing_name == easing_list[9]:
        return easeInQuint
    elif easing_name == easing_list[10]:
        return easeOutQuint
    elif easing_name == easing_list[11]:
        return easeInExpo
    elif easing_name == easing_list[12]:
        return easeOutExpo
    elif easing_name == easing_list[13]:
        return easeInCirc
    elif easing_name == easing_list[14]:
        return easeOutCirc


alt_state = 0


def save_file():
    global alt_state
    if dpg.get_value("md") == "overwrite":
        file = open(dpg.get_value("op"), 'w')
    else:
        file = open(dpg.get_value("op"), 'a')
    starttime = dpg.get_value("st")
    cursor = starttime
    endtime = dpg.get_value("et")
    interval = endtime - starttime
    step = dpg.get_value("iv")
    easing = pick_easing(dpg.get_value("es"))
    start_volume = dpg.get_value("sv")
    volume_change = dpg.get_value("ev") - start_volume

    slider_velocity = -100 / dpg.get_value("vs")
    slider_velocity = int(slider_velocity) if slider_velocity.is_integer() else slider_velocity
    sample_fix = dpg.get_value("sf")
    sample_alt = [dpg.get_value("sa1"), dpg.get_value("sa2")]
    kiai = 1 if dpg.get_value("ki") == "yes" else 0

    alt_mode = dpg.get_value("am")

    counter = alt_state
    seek = (cursor - starttime) / interval
    while cursor <= endtime:
        curr_volume = start_volume + int(round(easing(seek) * volume_change))
        if alt_mode == "sample index":
            file.write(f"{cursor},{slider_velocity},0,{sample_fix},{sample_alt[counter]},{curr_volume},0,{kiai}\n")
        else:
            file.write(f"{cursor},{slider_velocity},0,{sample_alt[counter]},{sample_fix},{curr_volume},0,{kiai}\n")

        cursor += step
        seek = (cursor - starttime) / interval
        while (abs(start_volume + int(round(easing(seek) * volume_change)) - curr_volume) < 1) and (cursor <= endtime):
            cursor += 1
            seek = (cursor - starttime) / interval
        counter += 1
        counter %= 2

    file.close()
    alt_state = counter

    with dpg.window(label="success?"):
        dpg.add_text("greenlines generated, manually copy to .osu")


def line_gen():
    global alt_state
    starttime = dpg.get_value("st")
    cursor = starttime
    endtime = dpg.get_value("et")
    interval = endtime - starttime
    step = dpg.get_value("iv")
    easing = pick_easing(dpg.get_value("es"))
    start_volume = dpg.get_value("sv")
    volume_change = dpg.get_value("ev") - start_volume

    slider_velocity = -100 / dpg.get_value("vs")
    slider_velocity = int(slider_velocity) if slider_velocity.is_integer() else slider_velocity
    sample_fix = dpg.get_value("sf")
    sample_alt = [dpg.get_value("sa1"), dpg.get_value("sa2")]
    kiai = 1 if dpg.get_value("ki") == "yes" else 0

    alt_mode = dpg.get_value("am")

    lines_out = []

    counter = alt_state
    seek = (cursor - starttime) / interval
    while cursor <= endtime:
        curr_volume = start_volume + int(round(easing(seek) * volume_change))
        if alt_mode == "sample index":
            lines_out.append(f"{cursor},{slider_velocity},0,{sample_fix},{sample_alt[counter]},{curr_volume},0,{kiai}\n")
        else:
            lines_out.append(f"{cursor},{slider_velocity},0,{sample_alt[counter]},{sample_fix},{curr_volume},0,{kiai}\n")

        cursor += step
        seek = (cursor - starttime) / interval
        while (abs(start_volume + int(round(easing(seek) * volume_change)) - curr_volume) < 1) and (cursor <= endtime):
            cursor += 1
            seek = (cursor - starttime) / interval
        counter += 1
        counter %= 2

    alt_state = counter

    return lines_out


def write_osu():
    file = dpg.get_value("op")
    with open(file, 'r+', encoding="utf-8") as fd:
        contents = fd.readlines()
        if "[TimingPoints]" in contents[-1]:  # Handle last line to prevent IndexError
            contents += line_gen()
        else:
            for index, line in enumerate(contents):
                if "[TimingPoints]" in line:
                    add_list = line_gen()
                    for dx, ins in enumerate(add_list):
                        contents.insert(index + 1 + dx, ins)
                    break
        fd.seek(0)
        fd.writelines(contents)


    with dpg.window(label="success?"):
        dpg.add_text("greenlines generated, god help you if its not utf-8")


def handle_output():
    if dpg.get_value("fm") == ".osu":
        write_osu()
    else:
        save_file()


def alternation_mode():
    if dpg.get_value("am") == "sample index":
        dpg.set_item_label("sf", "sample set")
        dpg.set_item_label("sa1", "sample index 1")
        dpg.set_item_label("sa2", "sample index 2")
    else:
        dpg.set_item_label("sf", "sample index")
        dpg.set_item_label("sa1", "sample set 1")
        dpg.set_item_label("sa2", "sample set 2")


def file_mode():
    if dpg.get_value("fm") == ".osu":
        dpg.set_item_label("op", ".osu location")
        dpg.show_item("cf")
        dpg.hide_item("md")
        dpg.set_value("op", "")
    else:
        dpg.set_item_label("op", "save to")
        dpg.hide_item("cf")
        dpg.show_item("md")
        dpg.set_value("op", "output.txt")


def file_select(app_data):
    dpg.set_value("op", dpg.get_file_dialog_info(app_data).get('file_path_name'))


dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.window(label="Generate volumes", width=800, height=600, tag="window"):
    dpg.add_text("Hello world")

    with dpg.collapsing_header(label="housekeeping(required)"):
        dpg.add_input_float(label="slider velocity", tag="vs", default_value=1)  # already used the tag sv oops
        dpg.add_input_int(label="sample set", tag="sf", default_value=0)
        dpg.add_combo(label="kiai", items=["yes", "no"], tag="ki", default_value="no")

    with dpg.collapsing_header(label="fun stuff"):
        dpg.add_input_int(label="start time(ms)", tag="st")
        dpg.add_input_int(label="end time(ms)", tag="et")
        dpg.add_input_int(label="start vol", tag="sv")
        dpg.add_input_int(label="end vol", tag="ev")
        dpg.add_combo(label="alternation mode", items=["sample index", "sample set"], tag="am",
                      default_value="sample index", callback=alternation_mode)
        dpg.add_input_int(label="sample index 1", tag="sa1", default_value=0)
        dpg.add_input_int(label="sample index 2", tag="sa2", default_value=1)
        dpg.add_input_int(label="minimum interval(lag prevention)", tag="iv", default_value=1)
        dpg.add_combo(label="easing", items=easing_list, tag="es", default_value="linear")

    with dpg.file_dialog(directory_selector=False, show=False, callback=file_select, id="file_dialog_id", width=700,
                         height=400):
        dpg.add_file_extension("", color=(150, 255, 150, 255))
        dpg.add_file_extension("Source files (*.osu){.osu}", color=(0, 255, 255, 255))

    with dpg.collapsing_header(label="do the thing", tag="go"):
        dpg.add_combo(label="file mode", items=[".osu", "external"], tag="fm", default_value="external",
                      callback=file_mode)
        dpg.add_combo(label="write mode", items=["append", "overwrite"], tag="md", default_value="overwrite")
        dpg.add_input_text(label="save to", tag="op", default_value="output.txt")
        dpg.add_button(label="choose file", tag="cf", show=False, callback=lambda: dpg.show_item("file_dialog_id"))
        dpg.add_button(label="Save", callback=handle_output)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
