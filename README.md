<h1 align="center">
  Midi Transcription
</h1>
<h3 align="center">An implementation of Score Transformer: Generating Musical Score from Note-level Representation</h3>
<h4 align="center">An attempt at transcribing midi notes to a musicxml file</h4>

## Instructions
Clone this repository:
```
git clone https://github.com/BarbosaRT/Midi-Translation.git
```
Access the directory:
```
cd Midi-Translation
```
Now install the dependencies:
```
pip install -r requirements.txt
```
To process the datasets included:
```
python3 main.py
```
If you want to train:
```
onmt_build_vocab -config mid_mxl.yaml -n_sample 40000 
```

```
onmt_train -config mid_mxl.yaml 
```

If you just want an Inference with the existing model:
- Download the model's weights [here](https://drive.google.com/file/d/1C4G8y4lrL6uLMNKZlNHv2gB55hz6SC5a/view?usp=sharing) and unzip the run folder inside the datasets directory
- Change the song file in tokenize_a_song.py, then:
```
python3 tokenize_a_song.py  
```

``` 
onmt_translate -model datasets/run/model_step_80000.pt -src tokens.txt -output pred.txt -gpu 0 -verbose  
```

``` 
python3 song_combiner.py   
```

## Notes
If you want to improve this code, feel free to do it. The trained model is ineffective at transcribing probably due to the lack of a large corpora of musical scores and also some problems with converting to tokens,
currently it doesn't support bpm changes it defaults the song's bpm to 120.   

## Citation:  
[Score Transformer: Generating Musical Score from Note-level Representation](https://arxiv.org/abs/2112.00355)  
``` 
@inproceedings{suzuki2021,  
 author = {Suzuki, Masahiro},  
 title = {Score Transformer: Generating Musical Score from Note-level Representation},  
 booktitle = {Proceedings of the 3rd ACM International Conference on Multimedia in Asia},  
 year = {2021},  
 pages = {31:1--31:7},  
 doi = {10.1145/3469877.3490612}  
}
```
