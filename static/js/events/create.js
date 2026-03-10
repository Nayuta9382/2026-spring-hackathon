
// チームを増減するスクリプト処理
function teamAddInput() {
    const container = document.getElementById('teams-container');

    // 行を作成
    const row = document.createElement('div');
    row.className = 'input-row';
    row.style.marginTop = '5px'; // 少し隙間をあける
    row.className = 'search-container min_space'

    // 入力欄を作成
    const input = document.createElement('input');
    input.type = 'text';
    input.name = 'teams';
    input.className = 'input_text';
    input.placeholder = `クラスチーム名を入力`;

    // 削除ボタンを作成
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.innerText = '削除';
    removeBtn.classList = 'delete btn delete_size';
    removeBtn.onclick = function() {
        row.remove(); // この行(div)を丸ごと削除

        // 2. 順位（ランクポイント）の一番下の行を削除
        const rankContainer = document.getElementById('rank-container');
        if (rankContainer.lastElementChild) {
            rankContainer.lastElementChild.remove();
        }
    };

    row.appendChild(input);
    row.appendChild(removeBtn);
    container.appendChild(row);
    
}

/**
 * セレクトボックスの値によってチーム入力欄の表示/非表示を切り替える
 */
function toggleTeamsDisplay() {
    const categorySelect = document.getElementById('id_category');
    const customArea = document.getElementById('custom-teams-area');
    const classMsg = document.getElementById('class-teams-msg');
    
    if (categorySelect.value === "0") {
        // 一般(0)の場合は入力欄を表示、メッセージを隠す
        customArea.style.display = 'block';
        classMsg.style.display = 'none';
    } else {
        // クラス対抗(1)の場合は入力欄を隠し、メッセージを表示
        customArea.style.display = 'none';
        classMsg.style.display = 'block';
    }
}

// ページ読み込み時に実行して現在の設定を反映
document.addEventListener('DOMContentLoaded', function() {
    toggleTeamsDisplay();
});

 (function() {
    // tournamentのimgプレビュー
    const fileInput = document.getElementById('tournament_input');
    const selectButton = document.getElementById('tournament_btn');
    const previewImage = document.getElementById('tournament_preview');

    // ボタンをクリックしたら隠れたinputを起動
    selectButton.addEventListener('click', () => {
        fileInput.click();
    });

    // ファイル選択時のプレビュー処理
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
            }
            reader.readAsDataURL(file);
        } else {
            // キャンセルされたらデフォルトに戻す
            previewImage.src = defaultSrc;
        }
    });
})();

// 競技画像プレビュー
(function() {
    const fileInput = document.getElementById('event_input');
    const selectButton = document.getElementById('event_btn');
    const previewImage = document.getElementById('event_preview');

    // ボタンをクリックして隠しinputを呼び出す
    selectButton.addEventListener('click', () => {
        fileInput.click();
    });

    // プレビュー表示の切り替え
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
            }
            reader.readAsDataURL(file);
        } else {
            // ファイル未選択時はデフォルトに戻す
            previewImage.src = defaultSrc;
        }
    });
})();
