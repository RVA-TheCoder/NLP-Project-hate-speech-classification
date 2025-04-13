from hate_speech.entity.config_entity import ModelTrainerConfig
from keras.models import Sequential
from keras.optimizers import RMSprop, Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint

from keras.layers import LSTM, Activation, Dense, Input, Embedding, SpatialDropout1D
from hate_speech.constants import *




# Creating Model Architecture
class ModelArchitecture:
    
    def __init__(self):
        pass
    
    def get_model(self):
        
        # Creating model architecture.
        model = Sequential()
        #model1.add(Embedding(max_words,100,input_length=max_len))
        model.add( Embedding(MAX_WORDS, 100) )
        model.add( SpatialDropout1D(0.2) )
        #model.add( LSTM(100,dropout=0.2,recurrent_dropout=0.2) )
        model.add( LSTM(100,dropout=0.2,) )
        model.add( Dense(1,activation=ACTIVATION) )
        model.summary()
        
        # Model compilation
        model.compile(loss=LOSS,
                      optimizer=Adam(),
                      metrics=METRICS
                      )
        
        return model
    












