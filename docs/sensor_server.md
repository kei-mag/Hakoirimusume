# �����薺�Z���T�[�T�[�o�[
�����薺�Z���T�[�T�[�o�[�́AHTTP���N�G�X�g�ɉ�����Raspberry Pi Camera Module�ŏ����̗l�q���B�e���ABME280�Z���T�[�ŉ��x�E���x�E�C�����擾���ĕԂ��T�[�o�[�ł��B

���̃v���O�������@�\��񋟂���ɂ�Camera Module��BME280�Z���T�[���K�v�ƂȂ邽�߁ARaspberry Pi��œ��삷�邱�Ƃ��z�肳��Ă��܂��B

## �Z���T�[�T�[�o�[�̎d�l
### �G���h�|�C���g
- `/` : �����̉��x�E���x�E�C����\������_�b�V���{�[�h�y�[�W
- `/get` : API���N�G�X�g�̃G���h�|�C���g�i�����薺LINE�{�b�g�T�[�o�[�͂��̃G���h�|�C���g�Ƀ��N�G�X�g�𑗐M���ď����擾���܂��j

### �_�b�V���{�[�h
�Z���T�[�T�[�o�[�́A���݂̏����̋C���E���x�E�C���̕\����A�V���b�g�_�E���{�^����\������_�b�V���{�[�h�y�[�W��񋟂��܂��B
- �_�b�V���{�[�h�Ŏg���Ă���HTML�e���v���[�g�́A`sensor_server/templates/dashboard.html`�ɂ���܂��B
- `dashboard.html`���ł͈ȉ��̃v���[�X�z���_�[�����ۂ̒l�ɒu�������ĕ\�����܂��B
  - `{{INTERVAL}}` : �_�b�V���{�[�h�̍X�V�Ԋu�i�b�j�C600�b�ɐݒ肵�Ă���܂��B 
  - `{{DATETIME}}` : �擾��������
  - `{{TEMP}}` : ���݂̋C��
  - `{{HUMID}}` : ���݂̎��x
  - `{{PRESS}}` : ���݂̋C��
- �V���b�g�_�E���{�^���������ƁA`/shutdown`��POST���N�G�X�g�𑗐M����Raspberry Pi���V���b�g�_�E�����܂��B
- �V���b�g�_�E���{�^���������ꂽ�ۂ̉�ʍ\���́A`sensor_server/templates/shuttingdown.html`�ɂ���܂��B
- �_�b�V���{�[�h�̉�ʍ\����[Kindle Paper white ��6����](https://www.amazon.co.jp/KindlePaperwhite-%E3%82%AD%E3%83%B3%E3%83%89%E3%83%AB-%E9%9B%BB%E5%AD%90%E6%9B%B8%E7%B1%8D%E3%83%AA%E3%83%BC%E3%83%80%E3%83%BC/dp/B00CTUMMD2/ref=cm_cr_arp_d_product_top?ie=UTF8)��[SkipStone Browser](http://www.fabiszewski.net/kindle-browser/)�ŕ\�������Ƃ��ɍœK�ɂȂ�悤�ɂȂ��Ă��܂��B
  ![Kindle���g�������x�v�_�b�V���{�[�h](images/thermometer_dashboard_kindle.jpg)

### API���N�G�X�g
HTTP GET��`/get`�Ƀ��N�G�X�g�𑗐M����ƁA�����̋C���E���x�E�C�����擾����JSON�`���ŕԂ��܂��B

#### ���N�G�X�g�p�����[�^�[
�P��`/get`�Ƀ��N�G�X�g�𑗐M�����ꍇ�ɂ͋C���E���x�E�C���̒l��Ԃ��܂��B  
`/get?withcamera`�Ƀ��N�G�X�g�𑗐M���邱�ƂŁA�J�����ŎB�e�����摜��URL���Ԃ��܂��B

#### ���X�|���X
JSON�`���ŕԂ���郌�X�|���X�͈ȉ��̂悤�Ȍ`���ł��B
```json
{
  "datetime": "2024-06-22T23:31:37+09:00",
  "temp": 25.717657079087802,
  "humid": 64.14656215454197,
  "press": 1001.6473936276144,
  "image": "http://imgur.com/xxxxxx.png",
  "deletehash": "xxxxxx"
}
```
| �t�B�[���h        | ����               | �⑫                                          |
|--------------|------------------|---------------------------------------------|
| `datetime`   | �擾��������           | ISO 8601�̃I�t�Z�b�g�`���̃^�C���X�^���v                    |
| `temp`       | �C��               | �P�ʁF��                                        |
| `humid`      | ���x               | �P�ʁF%                                        |
| `press`      | �C��               | �P�ʁFhPa                                      |
| `image`      | �����̉摜��Imgur URL  | `withcamera`�p�����[�^�[���Ȃ��ꍇ��null�܂��̓L�[���̂��܂܂�܂���B |
| `deletehash` | Imgur�摜�̍폜�p�n�b�V���l | `withcamera`�p�����[�^�[���Ȃ��ꍇ��null�܂��̓L�[���̂��܂܂�܂���B |
