void* fn_27_D9688(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 24) + i;
    if (idx >= 115) idx -= 115;
    return (char*)p + idx * 48 + 12;
}
