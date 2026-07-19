void* fn_27_D92F0(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 39) idx -= 39;
    return (char*)p + idx * 48 + 12;
}
