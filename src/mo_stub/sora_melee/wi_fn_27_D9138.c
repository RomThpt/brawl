void* fn_27_D9138(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 12) idx -= 12;
    return (char*)p + idx * 20 + 12;
}
