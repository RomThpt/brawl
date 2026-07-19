void* fn_27_D9070(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 8) idx -= 8;
    return (char*)p + idx * 52 + 12;
}
