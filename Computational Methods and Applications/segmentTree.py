import time
import random
import tqdm
import matplotlib.pyplot as plt

class SegmentTree:
    def __init__(self, arr):
        self.tree = [0] * (4 * len(arr))
        self.build_tree(arr, 1, 0, len(arr) - 1)

    def build_tree(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self.build_tree(arr, 2 * node, start, mid)
            self.build_tree(arr, 2 * node + 1, mid + 1, end)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] += val
        else:
            mid = (start + end) // 2
            if start <= idx and idx <= mid:
                self.update(2 * node, start, mid, idx, val)
            else:
                self.update(2 * node + 1, mid + 1, end, idx, val)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        p1 = self.query(2 * node, start, mid, l, r)
        p2 = self.query(2 * node + 1, mid + 1, end, l, r)
        return p1 + p2

def linear_update(arr, l, r, val):
    for i in range(l, r+1):
        arr[i] += val

def linear_query(arr, l, r):
    ans = 0
    for i in arr[l:r+1]:
        ans += i
    return ans

n = 100000
arr = [random.randint(1, 100) for i in range(n)]

t1 = time.time()
st = SegmentTree(arr)
t2 = time.time()
print(f"Time taken to build segment tree: {t2 - t1:.6f} seconds")


def plot(X):
    seg_upd = []
    seg_qry = []
    lin_upd = []
    lin_qry = []
    for up in tqdm.tqdm(X):
        t1 = time.time()
        st.update(1, 0, up, 5, 10)
        t2 = time.time()
        # print(f"Time taken for segment tree update: {t2 - t1:.6f} seconds")
        seg_upd.append(t2 - t1)

        t1 = time.time()
        st.query(1, 0, up, 10, 50)
        t2 = time.time()
        # print(f"Time taken for segment tree query: {t2 - t1:.6f} seconds")
        seg_qry.append(t2 - t1)

        t1 = time.time()
        linear_update(arr, 0, up, 10)
        t2 = time.time()
        # print(f"Time taken for linear update: {t2 - t1:.6f} seconds")
        lin_upd.append(t2 - t1)

        t1 = time.time()
        linear_query(arr, 0, up)
        t2 = time.time()
        # print(f"Time taken for linear query: {t2 - t1:.6f} seconds")
        lin_qry.append(t2 - t1)

    plt.plot(X,seg_upd,label='seg_upd')
    plt.plot(X,seg_qry,label='seg_qry')
    plt.plot(X,lin_upd,label='lin_upd')
    plt.plot(X,lin_qry,label='lin_qry')
    plt.title('Time taken vs range length')
    plt.xlabel('Range length')
    plt.ylabel('Time taken (s)')
    plt.legend()
    plt.show()

# X = [i for i in range(0,n-1,1000)]
# plot(X)
X = [i for i in range(0,100,1)]
plot(X)