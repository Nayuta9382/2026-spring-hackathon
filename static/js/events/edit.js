
// チームを増減するスクリプト処理
function teamAddInput() {
    const container = document.getElementById('teams-container');

    // 行を作成
    const row = document.createElement('div');
    row.className = 'input-row';
    row.style.marginTop = '5px'; // 少し隙間をあける

    // 入力欄を作成
    const input = document.createElement('input');
    input.type = 'text';
    input.name = 'teams';
    input.placeholder = `クラスチーム名を入力`;

    // 削除ボタンを作成
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.innerText = '×';
    removeBtn.style.marginLeft = '5px';
    removeBtn.onclick = function() { removeBtnEvent(this); };
    row.appendChild(input);
    row.appendChild(removeBtn);
    container.appendChild(row);
    
    rankAddInput();
}

function removeBtnEvent(btn) {
    // 1. ボタンの親要素（.input-row）を探して削除
    const row = btn.closest('.input-row');
    if (row) {
        row.remove();
    }

    // 2. ランクポイントの「最後の一行」を削除
    const rankContainer = document.getElementById('rank-container');
    if (rankContainer && rankContainer.lastElementChild) {
        rankContainer.lastElementChild.remove();
    }

  
}