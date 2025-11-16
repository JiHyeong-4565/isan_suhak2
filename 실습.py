import copy

def print_matrix(matrix, title="행렬"):
    """
    행렬을 보기 좋게 출력하는 함수
    :param matrix: 2D 리스트 (행렬)
    :param title: 출력할 행렬의 제목
    """
    print(f"\n--- {title} ---")
    if not matrix:
        print(" (빈 행렬)")
        return
    
    n = len(matrix)
    col_width = max(len(str(x)) for row in matrix for x in row) + 2
    
    # 헤더 (1 2 3 4 5)
    print("     " + "".join(f"{i+1:<{col_width}}" for i in range(n)))
    print("   " + "-" * (n * col_width + 5))
    
    for i in range(n):
        # 행 인덱스 (1 | 2 | ...)
        print(f" {i+1} | ", end="")
        for j in range(n):
            print(f"{matrix[i][j]:<{col_width}}", end="")
        print()
    print("-" * (n * col_width + 8))

def get_matrix(n):
    """
    사용자로부터 N x N 관계 행렬을 입력받는 함수 (기능 1)
    """
    print(f"집합 A = {{1, 2, 3, 4, 5}} (N={n}) 에 대한 관계 행렬을 입력합니다.")
    print("각 행의 원소(0 또는 1)를 띄어쓰기로 구분하여 5개씩 입력해주세요.")
    
    matrix = []
    for i in range(n):
        while True:
            try:
                row_input = input(f"  {i+1}번째 행 입력: ")
                row = [int(x) for x in row_input.split()]
                
                # 입력 개수 확인
                if len(row) != n:
                    print(f"  [오류] {n}개의 원소를 입력해야 합니다. (입력된 개수: {len(row)})")
                    continue
                
                # 0 또는 1인지 확인 (추가 기능: 입력 유효성 검사)
                if not all(x in [0, 1] for x in row):
                    print("  [오류] 0 또는 1만 입력할 수 있습니다.")
                    continue
                    
                matrix.append(row)
                break  # 성공적으로 입력받으면 while 루프 탈출
            
            except ValueError:
                print("  [오류] 숫자로만 입력해주세요.")
            except Exception as e:
                print(f"  [오류] 알 수 없는 오류: {e}")
                
    return matrix

# --- 동치 관계 판별 함수 (기능 2) ---

def is_reflexive(matrix, n):
    """
    반사 관계인지 판별
    - 모든 i에 대해 (i, i)가 관계에 속하는지 (matrix[i][i] == 1) 확인
    """
    for i in range(n):
        if matrix[i][i] == 0:
            return False
    return True

# (추가 기능) 비반사 관계 판별
def is_irreflexive(matrix, n):
    """
    (추가 기능) 비반사 관계인지 판별
    - 모든 i에 대해 (i, i)가 관계에 속하지 않는지 (matrix[i][i] == 0) 확인
    """
    for i in range(n):
        if matrix[i][i] == 1: # 하나라도 1이면 비반사가 아님
            return False
    return True

def is_symmetric(matrix, n):
    """
    대칭 관계인지 판별
    - 모든 (i, j)에 대해 (i, j)가 관계에 속하면 (j, i)도 속하는지
    - (matrix[i][j] == matrix[j][i]) 확인
    """
    for i in range(n):
        for j in range(i + 1, n):  # 중복 확인 피하기 (i < j)
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

def is_transitive(matrix, n):
    """
    추이 관계인지 판별 (Warshall 알고리즘과 유사)
    - (i, j)와 (j, k)가 관계에 속하면 (i, k)도 속하는지 확인
    """
    for i in range(n):
        for j in range(n):
            for k in range(n):
                # 만약 (i, j) 관계가 있고 (j, k) 관계가 있는데
                if matrix[i][j] == 1 and matrix[j][k] == 1:
                    # (i, k) 관계가 없다면 추이 관계가 아님
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
    """
    모든 관계 성질을 판별하고 결과를 출력 (기능 2)
    """
    print("\n[관계 성질 판별 결과]")
    
    is_ref = is_reflexive(matrix, n)
    is_sym = is_symmetric(matrix, n)
    is_tran = is_transitive(matrix, n)
    
    print(f"  - 반사 관계 (Reflexive) : {'O' if is_ref else 'X'}")
    print(f"  - 대칭 관계 (Symmetric) : {'O' if is_sym else 'X'}")
    print(f"  - 추이 관계 (Transitive): {'O' if is_tran else 'X'}")
    
    # (추가 기능) 반대칭, 비반사 관계 확인
    print("  --- (추가 기능 판별) ---")
    is_irref = is_irreflexive(matrix, n) # 비반사 호출
    is_anti = is_antisymmetric(matrix, n)
    print(f"  - 비반사 관계 (Irreflexive): {'O' if is_irref else 'X'}") # 비반사 출력
    print(f"  - 반대칭 관계 (Anti-symmetric): {'O' if is_anti else 'X'}")
    
    return is_ref, is_sym, is_tran

# --- 동치류 출력 함수 (기능 3) ---

def find_equivalence_classes(matrix, n):
    """
    동치 관계일 경우, 동치류를 찾아 출력 (기능 3)
    """
    print("\n[동치류 출력]")
    
    # visited 배열: 이미 동치류에 포함된 원소를 추적
    visited = [False] * n
    
    for i in range(n):
        # 아직 처리되지 않은 원소인 경우에만 동치류 계산
        if not visited[i]:
            equivalence_class = []
            for j in range(n):
                # matrix[i][j] == 1 이라는 것은 i와 j가 관계가 있다는 의미
                # 동치 관계이므로, i와 관계있는 모든 j가 i의 동치류에 속함
                if matrix[i][j] == 1:
                    equivalence_class.append(j + 1)
                    visited[j] = True  # j는 이제 처리된 것으로 표시
            
            # 집합 A의 원소는 1부터 시작
            print(f"  - 원소 {i+1}이(가) 포함된 동치류: {sorted(list(set(equivalence_class)))}")

# --- 폐포 구현 함수 (기능 4) ---

def reflexive_closure(matrix, n):
    """
    반사 폐포(r(R))를 계산
    - 대각 행렬을 모두 1로 만듦
    """
    # 원본이 바뀌지 않도록 깊은 복사
    r_closure = copy.deepcopy(matrix)
    for i in range(n):
        r_closure[i][i] = 1
    return r_closure

def symmetric_closure(matrix, n):
    """
    대칭 폐포(s(R))를 계산
    - (i, j)가 1이면 (j, i)도 1로 만듦
    """
    s_closure = copy.deepcopy(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            if s_closure[i][j] == 1:
                s_closure[j][i] = 1
            elif s_closure[j][i] == 1:
                s_closure[i][j] = 1
    return s_closure

def transitive_closure(matrix, n):
    """
    추이 폐포(t(R))를 계산 (Warshall's Algorithm)
    - R* = R U R^2 U ... U R^n
    """
    t_closure = copy.deepcopy(matrix)
    
    # k: 중간 정점
    for k in range(n):
        # i: 시작 정점
        for i in range(n):
            # j: 끝 정점
            for j in range(n):
                # (i, k) 경로와 (k, j) 경로가 있다면 (i, j) 경로도 있음을 의미
                # t_closure[i][j] = t_closure[i][j] OR (t_closure[i][k] AND t_closure[k][j])
                t_closure[i][j] = t_closure[i][j] or (t_closure[i][k] and t_closure[j][k])
                # 파이썬 bool(True/False)은 int(1/0)로 자동 형변환됨
                # 명시적으로 int로 변환
                t_closure[i][j] = int(t_closure[i][j])
                
    return t_closure

# --- 메인 실행 함수 ---
def main():
    N = 5  # 집합 A의 원소 개수
    
    # 1. 관계 행렬 입력
    original_matrix = get_matrix(N)
    print_matrix(original_matrix, "입력된 관계 행렬 (Original Relation)")
    
    # 2. 동치 관계 판별
    is_ref, is_sym, is_tran = check_all_properties(original_matrix, N)
    
    print("-" * 30)
    if is_ref and is_sym and is_tran:
        print(">>> 최종 판별: 동치 관계(Equivalence Relation)입니다.")
        # 3. 동치류 출력
        find_equivalence_classes(original_matrix, N)
    else:
        print(">>> 최종 판별: 동치 관계가 아닙니다.")
        print("입력된 관계에 대한 폐포를 계산하여 동치 폐포를 생성합니다.")
        
        # 4. 폐포 구현
        
        # r(R) : 반사 폐포
        print("\n=== 4-1. 반사 폐포 (Reflexive Closure) ===")
        r_closure = reflexive_closure(original_matrix, N)
        if not is_ref:
            print("  [변환 전 행렬 (Original)]")
            print_matrix(original_matrix, "Original")
            print("  [변환 후 행렬 (Reflexive Closure)]")
            print_matrix(r_closure, "r(R)")
        else:
            print("  - 이미 반사 관계를 만족하므로 변환이 필요하지 않습니다.")
        
        # s(r(R)) : 대칭 폐포
        print("\n=== 4-2. 대칭 폐포 (Symmetric Closure) ===")
        s_closure = symmetric_closure(r_closure, N)
        # s(r(R))가 r(R)과 다른지 확인하여 출력
        if not is_symmetric(r_closure, N): 
            print("  [변환 전 행렬 (r(R))]")
            print_matrix(r_closure, "r(R)")
            print("  [변환 후 행렬 (Symmetric Closure on r(R))]")
            print_matrix(s_closure, "s(r(R))")
        else:
            print("  - 반사 폐포가 이미 대칭 관계를 만족하므로 변환이 필요하지 않습니다.")
            
        # t(s(r(R))) : 추이 폐포 (이것이 동치 폐포)
        print("\n=== 4-3. 추이 폐포 (Transitive Closure) ===")
        equivalence_closure = transitive_closure(s_closure, N)
        if not is_transitive(s_closure, N):
            print("  [변환 전 행렬 (s(r(R)))]")
            print_matrix(s_closure, "s(r(R))")
            print("  [변환 후 행렬 (Transitive Closure on s(r(R)))]")
            print_matrix(equivalence_closure, "t(s(r(R))) - Equivalence Closure")
        else:
            print("  - 대칭 폐포가 이미 추이 관계를 만족하므로 변환이 필요하지 않습니다.")
            
        # 5. 최종 동치 폐포 확인 및 동치류 출력
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
            # 이 메시지는 t(s(r(R))) 순서로 적용했다면 논리적으로 출력될 수 없습니다.
            print(">>> [오류] 동치 폐포 생성에 실패했습니다.")

if __name__ == "__main__":
    main()