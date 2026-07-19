extern char lbl_100_data_64F8;

void fn_100_DDA0(void* p) {
    *(void**)((char*)p + 0) = &lbl_100_data_64F8;
}
