# Set the target temp range here
min_temp_in_celsius = -10.0
max_temp_in_celsius = 60.0


def map_g_to_temp(g):
    return ((g * (max_temp_in_celsius - min_temp_in_celsius)) / 255.0) + min_temp_in_celsius
