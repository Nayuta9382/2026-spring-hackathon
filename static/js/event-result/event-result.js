document.addEventListener('DOMContentLoaded', function() {
    // プルダウン要素を取得
    const teamSelect = document.querySelector('select[name="class-team-flg"]');
    
    function updateDisplay() {
        let isYes;
        if (!teamSelect) {
            isYes = "0"
        }else{
            isYes = teamSelect.value === "1";
        }
        // すべてのスコア入力エリアを取得
        const pointAreas = document.querySelectorAll('.point-area');
        
        pointAreas.forEach(area => {
            const input = area.querySelector('.point-input');
            const span = area.querySelector('.point-display');
            
            if (!isYes) {
                // Yes の場合: 入力欄を表示、スパンを隠す
                input.style.display = "inline-block";
                span.style.display = "none";
            } else {
                // No の場合: 入力欄を隠し、スパンを表示
                input.style.display = "none";
                span.style.display = "inline-block";
            }
        });
    }

    // 初期表示の切り替え
    updateDisplay();

    if (teamSelect){
        // プルダウン変更時に実行
        teamSelect.addEventListener('change', updateDisplay);
    } 

});