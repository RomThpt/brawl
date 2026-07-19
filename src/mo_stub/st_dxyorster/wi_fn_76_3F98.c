void* fn_76_3F98(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 9) idx -= 9;
    return (char*)p + idx * 104 + 12;
}
