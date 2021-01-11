# Define install path

ROOT_DIR = /home/robert/redfish/Redfish_creater/swig
LIB_DIR = $(ROOT_DIR)/input
OBJ_DIR = $(ROOT_DIR)/output
PYTHON3.5_DIR = /usr/include/python3.5
CFLAGS = -fPIC -shared

.PHONY: all
all:
	@echo "Compileing ... "
	@echo "\n##########################################################"
	@echo "Build wrap file"
	@echo "##########################################################"
	swig -python $(LIB_DIR)/interface.i
	swig -python $(LIB_DIR)/interface1.i
	@echo "##########################################################"
	gcc $(CFLAGS) $(LIB_DIR)/interface_wrap.c $(LIB_DIR)/speedup_performance.c  -I$(PYTHON3.5_DIR) -o $(OBJ_DIR)/_test1.so
	gcc $(CFLAGS) $(LIB_DIR)/interface1_wrap.c $(LIB_DIR)/speedup_performance.c  -I$(PYTHON3.5_DIR) -o $(OBJ_DIR)/_test2.so
	
	@echo "##########################################################"
	@echo "mv py_file into output dir"
	mv $(LIB_DIR)/test2.py $(OBJ_DIR)/test2.py
	mv $(LIB_DIR)/test1.py $(OBJ_DIR)/test1.py

