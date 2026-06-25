#? score.py handles points allocation, streak combos, and highscore tracking
import json
import os

class ScoreManager: 
    def __init__(self):
        self.score=     0
        self.combo=     0
        self.high_score=0
        self.save_file= "save_data.json"
        self.load_high_score()

    def update(self,piece,cleared_lines): # calculates points for blocks placed and rewards consecutive line clears
        block_count=sum(1 for r in piece for cell in r if cell["tile"])
        self.score+=block_count

        if cleared_lines>0:
            self.score+=(cleared_lines*10)+(self.combo*5)
            self.combo+=1
        else:
            self.combo=0

        if self.score>self.high_score:
            self.high_score=self.score
            self.save_high_score()

    def load_high_score(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file,"r") as f:
                    data=json.load(f)
                    self.high_score=data.get("high_score",0)
            except:
                self.high_score=0

    def save_high_score(self):
        data={"high_score":self.high_score}
        try:
            with open(self.save_file,"w") as f:
                json.dump(data,f)
        except:
            pass

    def delete_save(self): # for the settings clear data button
        if os.path.exists(self.save_file):
            try:
                os.remove(self.save_file)
            except:
                pass
        self.high_score=0