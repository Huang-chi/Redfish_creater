#Define install path

ROOT_DIR = /home/robert/redfish/test_redfish/lib/private/ctype
LIB_DIR  = $(ROOT_DIR)/input
OBJ_DIR  = $(ROOT_DIR)/output

all:
	@echo "Compiling ..."
	@echo "\n#################################################"
	@echo "Build dynamic library"
	@echo "#################################################\n"
	
	@echo $(OBJ_DIR)
	gcc -shared -fPIC -o $(OBJ_DIR)/libtest.so $(LIB_DIR)/test_a.c $(LIB_DIR)/test_b.c $(LIB_DIR)/test_c.c $(LIB_DIR)/test_send_data.c
	
	gcc $(LIB_DIR)/test.c -L$(OBJ_DIR) -ltest -o test	
	
	@echo "\n#################################################"
	@echo "Build machine code (*.o)"
	@echo "#################################################\n"
	gcc -o $(OBJ_DIR)/test.o -c $(LIB_DIR)/test.c
	
	@echo "\n################################################"
	@echo "Build rpath"
	@echo "#################################################\n"
	gcc -o test $(OBJ_DIR)/test.o -L$(OBJ_DIR) -ltest -Wl,-rpath=$(OBJ_DIR)
	
	@echo "\n#################################################"
	@echo "Check file info "
	@echo "#################################################\n"
	ldd test
