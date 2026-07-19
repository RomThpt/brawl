void* fn_27_D9188(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 9) idx -= 9;
    return (char*)p + idx * 48 + 12;
}
