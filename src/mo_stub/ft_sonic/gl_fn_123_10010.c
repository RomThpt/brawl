extern char lbl_123_data_64B8;

void fn_123_10010(void* p) {
    *(void**)((char*)p + 0) = &lbl_123_data_64B8;
}
