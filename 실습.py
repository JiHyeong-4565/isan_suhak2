import copy

def print_matrix(matrix, title="행렬"):
    print(f"\n--- {title} ---")
    if not matrix:
        print(" (빈 행렬)")
        return
    
    n = len(matrix)
    col_width = max(len(str(x)) for row in matrix for x in row) + 2
    
    print("     " + "".join(f"{i+1:<{col_width}}" for i in range(n)))
    print("   " + "-" * (n * col_width + 5))
    
    for i in range(n):
        print(f" {i+1} | ", end="")
        for j in range(n):
            print(f"{matrix[i][j]:<{col_width}}", end="")
        print()
    print("-" * (n * col_width + 8))

def get_matrix(n):
    print(f"집합 A = {{1, 2, 3, 4, 5}} (N={n}) 에 대한 관계 행렬을 입력합니다.")
    print("각 행의 원소(0 또는 1)를 띄어쓰기로 구분하여 5개씩 입력해주세요.")
    
    matrix = []
    for i in range(n):
        while True:
            try:
                row_input = input(f"  {i+1}번째 행 입력: ")
                row = [int(x) for x in row_input.split()]
                
                if len(row) != n:
                    print(f"  [오류] {n}개의 원소를 입력해야 합니다. (입력된 개수: {len(row)})")
                    continue
                
                if not all(x in [0, 1] for x in row):
                    print("  [오류] 0 또는 1만 입력할 수 있습니다.")
                    continue
                    
                matrix.append(row)
                break
            
            except ValueError:
                print("  [오류] 숫자로만 입력해주세요.")
            except Exception as e:
                print(f"  [오류] 알 수 없는 오류: {e}")
                
    return matrix

def is_reflexive(matrix, n):
    for i in range(n):
        if matrix[i][i] == 0:
            return False
    return True

def is_irreflexive(matrix, n):
    for i in range(n):
        if matrix[i][i] == 1:
            return False
    return True

def is_symmetric(matrix, n):
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

def is_transitive(matrix, n):
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if matrix[i][j] == 1 and matrix[j][k] == 1:
                    if matrix[i][k] == 0:
                        return False
    return True

def is_antisymmetric(matrix, n):
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] == 1 and matrix[j][i] == 1:
                return False
    return True

def check_all_properties(matrix, n):
    print("\n[관계 성질 판별 결과]")
    
    is_ref = is_reflexive(matrix, n)
    is_sym = is_symmetric(matrix, n)
    is_tran = is_transitive(matrix, n)
    
    print(f"  - 반사 관계 (Reflexive) : {'O' if is_ref else 'X'}")
    print(f"  - 대칭 관계 (Symmetric) : {'O' if is_sym else 'X'}")
    print(f"  - 추이 관계 (Transitive): {'O' if is_tran else 'X'}")
    
    print("  --- (추가 기능 판별) ---")
    is_irref = is_irreflexive(matrix, n)
    is_anti = is_antisymmetric(matrix, n)
    print(f"  - 비반사 관계 (Irreflexive): {'O' if is_irref else 'X'}")
    print(f"  - 반대칭 관계 (Anti-symmetric): {'O' if is_anti else 'X'}")
    
    return is_ref, is_sym, is_tran

def find_equivalence_classes(matrix, n):
    print("\n[동치류 출력]")
    
    visited = [False] * n
    
    for i in range(n):
        if not visited[i]:
            equivalence_class = []
            for j in range(n):
                if matrix[i][j] == 1:
                    equivalence_class.append(j + 1)
                    visited[j] = True
            
            print(f"  - 원소 {i+1}이(가) 포함된 동치류: {sorted(list(set(equivalence_class)))}")

def reflexive_closure(matrix, n):
    r_closure = copy.deepcopy(matrix)
    for i in range(n):
        r_closure[i][i] = 1
    return r_closure

def symmetric_closure(matrix, n):
    s_closure = copy.deepcopy(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            if s_closure[i][j] == 1:
                s_closure[j][i] = 1
            elif s_closure[j][i] == 1:
                s_closure[i][j] = 1
    return s_closure

def transitive_closure(matrix, n):
    t_closure = copy.deepcopy(matrix)
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                t_closure[i][j] = t_closure[i][j] or (t_closure[i][k] and t_closure[j][k])
                t_closure[i][j] = int(t_closure[i][j])
                
    return t_closure

def main():
    N = 5
    
    original_matrix = get_matrix(N)
    print_matrix(original_matrix, "입력된 관계 행렬 (Original Relation)")
    
    is_ref, is_sym, is_tran = check_all_properties(original_matrix, N)
    
    print("-" * 30)
    if is_ref and is_sym and is_tran:
        print(">>> 최종 판별: 동치 관계(Equivalence Relation)입니다.")
        find_equivalence_classes(original_matrix, N)
    else:
        print(">>> 최종 판별: 동치 관계가 아닙니다.")
        print("입력된 관계에 대한 폐포를 계산하여 동치 폐포를 생성합니다.")
        
        print("\n=== 4-1. 반사 폐포 (Reflexive Closure) ===")
        r_closure = reflexive_closure(original_matrix, N)
        if not is_ref:
            print("  [변환 전 행렬 (Original)]")
            print_matrix(original_matrix, "Original")
            print("  [변환 후 행렬 (Reflexive Closure)]")
            print_matrix(r_closure, "r(R)")
        else:
            print("  - 이미 반사 관계를 만족하므로 변환이 필요하지 않습니다.")
        
        print("\n=== 4-2. 대칭 폐포 (Symmetric Closure) ===")
        s_closure = symmetric_closure(r_closure, N)
        if not is_symmetric(r_closure, N): 
            print("  [변환 전 행렬 (r(R))]")
            print_matrix(r_closure, "r(R)")
            print("  [변환 후 행렬 (Symmetric Closure on r(R))]")
            print_matrix(s_closure, "s(r(R))")
        else:
            print("  - 반사 폐포가 이미 대칭 관계를 만족하므로 변환이 필요하지 않습니다.")
            
        print("\n=== 4-3. 추이 폐포 (Transitive Closure) ===")
        equivalence_closure = transitive_closure(s_closure, N)
        if not is_transitive(s_closure, N):
            print("  [변환 전 행렬 (s(r(R)))]")
            print_matrix(s_closure, "s(r(R))")
            print("  [변환 후 행렬 (Transitive Closure on s(r(R)))]")
            print_matrix(equivalence_closure, "t(s(r(R))) - Equivalence Closure")
        else:
            print("  - 대칭 폐포가 이미 추이 관계를 만족하므로 변환이 필요하지 않습니다.")
            
        print("\n" + "=" * 30)
        print("  최종 동치 폐포 행렬: t(s(r(R)))")
        print("=" * 30)
        print_matrix(equivalence_closure, "최종 동치 폐포 (Equivalence Closure)")
        
        print("\n[최종 동치 폐포 행렬의 관계 성질 재확인]")
        final_ref, final_sym, final_tran = check_all_properties(equivalence_closure, N)
        
        if final_ref and final_sym and final_tran:
            print(">>> 최종 판별: 동치 폐포가 동치 관계임을 확인했습니다.")
            find_equivalence_classes(equivalence_closure, N)
        else:
            print(">>> [오류] 동치 폐포 생성에 실패했습니다.")

if __name__ == "__main__":
    main()
