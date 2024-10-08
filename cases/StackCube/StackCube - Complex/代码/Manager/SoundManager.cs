using UnityEngine;

public class SoundManager : Singleton<SoundManager>
{
    [SerializeField] AudioSource _bgMusicSource;

    [Space(10)]
    [Range(0, 1)] [SerializeField] float _musicVolume = 1f;
    [Range(0, 1)] [SerializeField] float _fxVolume = 1f;

    [Header("Audio Data")]
    [SerializeField] AudioDataSO _audioData;

    bool _musicEnable = true;
    bool _fxEnable = true;

    GameObject oneShotGameObject;
    AudioSource oneShotAudioSource;

    private void Start()
    {
        _musicEnable = SaveData.GetMusicState();
        _fxEnable = SaveData.GetSfxState();

        if (_musicEnable) PlayBackgroundMusic();
    }

    public void PlayAudio(AudioType type)
    {
        // return if audio fx is disable
        if (!_fxEnable) return;

        if (oneShotGameObject == null)
        {
            oneShotGameObject = new GameObject("Sound");
            oneShotAudioSource = oneShotGameObject.AddComponent<AudioSource>();
        }

        AudioClip clip = GetClip(type);
        oneShotAudioSource.volume = _fxVolume;
        oneShotAudioSource.PlayOneShot(clip);
    }

    public void ToggleMusic()
    {
        _musicEnable = !_musicEnable;
        UpdateMusic();

        SaveData.SetMusicState(_musicEnable);
    }

    public void ToggleFX()
    {
        _fxEnable = !_fxEnable;

        SaveData.SetSfxState(_fxEnable);
    }

    // private method
    void PlayBackgroundMusic()
    {
        _bgMusicSource.Stop();
        _bgMusicSource.clip = _audioData.BackgroundMusic;
        _bgMusicSource.volume = _musicVolume;
        _bgMusicSource.Play();
    }

    void UpdateMusic()
    {
        if (!_musicEnable)
            _bgMusicSource.Stop();
        else
            PlayBackgroundMusic();
    }

    AudioClip GetClip(AudioType type)
    {
        switch (type)
        {
            case AudioType.BACKGROUND:
                return _audioData.BackgroundMusic;
            case AudioType.PERFECT:
                return _audioData.PerfectClip;
            case AudioType.DROP:
                return _audioData.DropClip;
            case AudioType.GAMEOVER:
                return _audioData.GameOverClip;
            case AudioType.POP:
                return _audioData.PopClip;
            default:
                return _audioData.FailClip;
        }
    }
}


public enum AudioType
{
    BACKGROUND, PERFECT, DROP, GAMEOVER, POP, FAIL
}
