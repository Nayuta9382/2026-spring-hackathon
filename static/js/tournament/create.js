
// 大会作成の順位のinput要素を増減する
function rankAddInput() {
    const container = document.getElementById('rank-container');
    const currentCount = container.getElementsByClassName('input-row').length + 1;

    // 行（ラッパー）を作成
    const row = document.createElement('div');
    row.className = 'input-row';

    // Labelを作成
    const label = document.createElement('label');
    label.innerText = `${currentCount}位: `;

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
        if (label) label.innerText = `${rank}位: `;
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
    input.placeholder = `クラスチーム名を入力`;

    // 削除ボタンを作成
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.innerText = '×';
    removeBtn.style.marginLeft = '5px';
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
    
    rankAddInput();
}