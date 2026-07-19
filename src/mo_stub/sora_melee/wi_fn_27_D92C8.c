void* fn_27_D92C8(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 43) idx -= 43;
    return (char*)p + idx * 48 + 12;
}
