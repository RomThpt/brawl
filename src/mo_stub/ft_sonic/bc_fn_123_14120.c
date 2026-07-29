void fn_123_14120(void* p, int v) {
    *(int*)((char*)p + 16) = v;
    *(int*)((char*)p + 12) = v;
    *(int*)((char*)p + 8) = v;
}
