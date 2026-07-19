void* fn_27_1AFCEC(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 303) idx -= 303;
    return (char*)p + idx * 4 + 12;
}
