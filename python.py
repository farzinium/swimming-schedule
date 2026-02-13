from convertdate import persian
import datetime, json

# -------- تنظیمات اولیه --------
start_date_str = '1404/11/24'  # شروع برنامه
units = ['واحد ۱','واحد ۲','واحد ۳','واحد ۴','واحد ۵','واحد ۶','واحد ۷','واحد ۸','واحد ۹','واحد ۱۰','واحد ۱۱','واحد ۱۲','واحد ۱۳','واحد ۱۴','واحد ۱۶']  # واحدهای فعال
shift = 0
months_ahead = 3

# -------- کمکی: تبدیل ارقام به فارسی --------
def to_persian_digits(s):
    english_digits = "0123456789"
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    return s.translate(str.maketrans(english_digits, persian_digits))

# -------- کمکی: تبدیل جلالی به میلادی --------
def jalali_to_gregorian(jy, jm, jd):
    g_y, g_m, g_d = persian.to_gregorian(jy, jm, jd)
    return datetime.date(g_y, g_m, g_d)

# -------- کمکی: تبدیل میلادی به جلالی --------
def gregorian_to_jalali(date):
    j_y, j_m, j_d = persian.from_gregorian(date.year, date.month, date.day)
    return j_y, j_m, j_d

# -------- کمکی: روز هفته فارسی --------
persian_weekdays = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یک‌شنبه"]

def weekday_persian(date):
    wd = date.weekday()  # Monday=0
    return persian_weekdays[wd % 7]

# -------- تولید بازه‌ی سه‌ماهه تاریخ‌ها (به جز جمعه‌ها) --------
sy, sm, sd = map(int, start_date_str.split('/'))
start_g = jalali_to_gregorian(sy, sm, sd)
end_g = start_g + datetime.timedelta(days=90)

all_days = []
cur = start_g
while cur <= end_g:
    j_y, j_m, j_d = gregorian_to_jalali(cur)
    wd = weekday_persian(cur)
    if wd != "جمعه":
        all_days.append((f"{j_y:04}/{j_m:02}/{j_d:02}", wd))
    cur += datetime.timedelta(days=1)

# -------- ساخت نوبت‌ها --------
loop_units = units.copy()
is_even = (len(loop_units) % 2 == 0)
index = shift
swap_flag = False

schedule = []

for i, (jal, wd) in enumerate(all_days):
    if index >= len(loop_units):
        index = index % len(loop_units)

    u1 = loop_units[index % len(loop_units)]
    u2 = loop_units[(index + 1) % len(loop_units)]
    
    slot1_unit = u1
    slot2_unit = u2

    schedule.append({
        "date": to_persian_digits(jal),
        "weekday": wd,
        "slot1_unit": slot1_unit,
        "slot2_unit": slot2_unit,
    })

    index += 2

# -------- ذخیره در فایل JSON --------
output_path = 'schedule.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(schedule, f, ensure_ascii=False, indent=2)