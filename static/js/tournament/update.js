// 大会作成の順位のinput要素を増減する
function rankAddInput() {
    const container = document.getElementById('rank-container');
    const currentCount = container.getElementsByClassName('input-row').length + 1;

    // 行（ラッパー）を作成
    const row = document.createElement('div');
    row.className = 'input-row';

    // Labelを作成
    const label = document.createElement('label');
    label.innerHTML = `<h2>${currentCount}位</h2>`;

    // 入力欄を作成
    const input = document.createElement('input');
    input.type = 'number';
    input.name = 'rank_points';
    input.placeholder = `${currentCount}位のポイント`;
    input.value = 0

    row.appendChild(label);
    row.appendChild(input);
    container.appendChild(row);
}

// 大会作成の順位とプレースホルダーを再計算する関数
function updateRankLabels() {
    const rows = document.getElementById('rank-container').getElementsByClassName('input-row');
    Array.from(rows).forEach((row, index) => {
        const rank = index + 1;
        // ラベルを更新
        const label = row.querySelector('label');
        if (label) label.innerHTML = `<h2>${currentCount}位</h2>`;
        // プレースホルダーも更新
        const input = row.querySelector('input');
        if (input) input.placeholder = `${rank}位のポイント`;
    });
}


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
    input.className = 'class_team_input';
    input.placeholder = `クラスチーム名を入力`;

    // 削除ボタンを作成
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.innerText = '削除';
    removeBtn.style.marginLeft = '1rem';
    removeBtn.className = 'delete_btn';
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

    // 3. 順位のラベル（1位、2位...）を再計算して整える
    updateRankLabels();
}
