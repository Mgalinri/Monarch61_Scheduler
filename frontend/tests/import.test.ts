describe('import vue components', () => {
    test('normal imports as expected', async () => {
        const cmp = await import('../pages/Homepage.vue')
        expect(cmp).toBeDefined()
    }),
    test('adding two numbers', async () => {
        const data = {one: 1 , two:2};
        data['one'] = 1;
        expect(data).toEqual({one: 1, two: 2});
    })
})