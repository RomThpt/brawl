void* fn_56_65B4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 30) + i;
    if (idx >= 1) idx -= 1;
    return (char*)p + idx * 144 + 12;
}
