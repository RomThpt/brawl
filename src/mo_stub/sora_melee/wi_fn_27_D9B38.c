void* fn_27_D9B38(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 11) idx -= 11;
    return (char*)p + idx * 36 + 12;
}
