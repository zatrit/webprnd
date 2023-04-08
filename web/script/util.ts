/** https://stackoverflow.com/a/31973533/12245612 */
export function pairwise<T>(arr: T[], func: (cur: T, next: T) => void) {
    for (let i = 0; i < arr.length - 1; i++) {
        func(arr[i], arr[i + 1]);
    }
}