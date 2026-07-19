void* fn_27_1AFEA4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 283) idx -= 283;
    return (char*)p + idx * 4 + 12;
}
