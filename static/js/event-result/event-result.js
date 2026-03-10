document.addEventListener('DOMContentLoaded', function() {
    // プルダウン要素を取得
    const teamSelect = document.querySelector('select[name="class-team-flg"]');
    console.log("cc");
    
    function updateDisplay() {
        let isYes;
        if (!teamSelect) {
            isYes = false;
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
                // クラス順位ポイントを表示する
                applyRankPoints();
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



// クラス順位ポイント使用時にクラス順位ポイントを表示する関数
function applyRankPoints() {
    const pointAreas = document.querySelectorAll('.point-area');

    pointAreas.forEach(area => {
        const rankSelect = area.previousElementSibling.querySelector('.rank-select');
        const display = area.querySelector('.point-display');

        if (rankSelect && display) {
            // 順位(rank)を取得
            const currentRank = rankSelect.value;
            // JSONからポイントを引き、spanに反映
            display.textContent = rankPoints[parseInt(currentRank)] || 0;

        }
    });
}


// 順位変更時にポイントの更新描画する
const rankSelects = document.querySelectorAll('.rank-select');

rankSelects.forEach(select => {
    select.addEventListener('change', function() {
       applyRankPoints();
    });
});