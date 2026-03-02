

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

    };

    row.appendChild(input);
    row.appendChild(removeBtn);
    container.appendChild(row);
    
}