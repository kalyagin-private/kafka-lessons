from jinja2 import Template
import sys

example={
    "Alloc": {
        "Type": "gauge",
        "Name": "Alloc",
        "Description": "Alloc is bytes of allocated heap objects.",
        "Value": 24293912
    },
    "FreeMemory": {
        "Type": "gauge",
        "Name": "FreeMemory",
        "Description": "RAM available for programs to allocate",
        "Value": 7740977152
    },
    "PollCount": {
        "Type": "counter",
        "Name": "PollCount",
        "Description": "PollCount is quantity of metrics collection iteration.",
        "Value": 3
    },
    "TotalMemory": {
        "Type": "gauge",
        "Name": "TotalMemory",
        "Description": "Total amount of RAM on this system",
        "Value": 16054480896
    }
}

# # HELP Alloc Alloc is bytes of allocated heap objects.
# # TYPE Alloc gauge
# Alloc 2.427184e+07
# # HELP FreeMemory RAM available for programs to allocate
# # TYPE FreeMemory gauge
# FreeMemory 7.740977152e+09
# # HELP PollCount PollCount is quantity of metrics collection iteration.
# # TYPE PollCount counter
# PollCount 1
# # HELP TotalMemory Total amount of RAM on this system
# # TYPE TotalMemory gauge
# TotalMemory 1.6054480896e+10

# Шаблон для отображения информации о работниках
metrics_template = """
{% for key, value in metrics.items() %}
{{ value['Name'] }}{{ '{' }}{{ 'type' }}="{{ value['Type'] }}",{{ 'description' }}="{{ value['Description'] }}"{{ '}' }} {{ value['Value'] }}
{% endfor %}
"""

metrics_template_v2 = """{% for key, value in metrics.items() -%}
{{ '# HELP' }} {{ value['Name'] }} {{ value['Description'] }}
{{ '# TYPE' }} {{ value['Name'] }} {{ value['Type'] }}
{{ value['Name'] }} {{ value['Value'] }}
{% endfor -%}"""

def render_metrics(metrics):
   # Создание шаблона
   tmpl = Template(metrics_template_v2)
   # Выполнение шаблона и вывод результата
   try:
       output = tmpl.render(metrics=metrics)
       return output
   except Exception as e:
       print(f"Ошибка при выполнении шаблона: {e}", file=sys.stderr)



# print(render_metrics(metric))