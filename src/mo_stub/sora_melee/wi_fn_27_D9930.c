void* fn_27_D9930(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 11) idx -= 11;
    return (char*)p + idx * 52 + 12;
}
