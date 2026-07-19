void* fn_27_D9610(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 23) + i;
    if (idx >= 146) idx -= 146;
    return (char*)p + idx * 48 + 12;
}
