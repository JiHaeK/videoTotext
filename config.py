IMAGE_CONFIG = {
    "resize_origin":
	{
		"standard_width": 512,
		"standard_height": 512
	},
	"gradient": 
	{
		"kernel_size_row":3,
		"kernel_size_col":3
	},
	"threshold": 
	{
		"mode": "gaussian",
		"block_size":15,
		"subtract_val": 21

	},
	"remove_line":
	{
		"threshold": 200,
		"min_line_length": 53, 
		"max_line_gap": 200
	},
	"close": 
	{
		"kernel_size_row": 25,
		"kernel_size_col": 10
	},
	"contour":
	{
		"min_width": 100,
		"min_height": 15,
		"section_x": 90,
		"section_y": 60,
		"padding": 2
	}
}

RECO_CONFIG = {
    "tesseract": '/usr/local/Cellar/tesseract/4.1.0/bin/tesseract',
    "custom_oem_psm_config" : '--oem 3 --psm 6',
    "custom_config": '--psm 1 -c preserve_interword_spaces=1',
    "lang": 'kor'
}
