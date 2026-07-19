void* fn_27_2EAC28(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 29) + i;
    if (idx >= 3) idx -= 3;
    return (char*)p + idx * 12 + 28;
}
