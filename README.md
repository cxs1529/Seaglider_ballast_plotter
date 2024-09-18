# Seaglider_ballast_plotter
Script to check Seaglider operation ranges, CVBD, and achievable densities.  

![Ballasting_plot](https://github.com/user-attachments/assets/9c54a2f1-70c4-4676-b99d-12658cc55e22)


- The central blue line is the operation range for the given CVBD (2700 here) and water density (sigmaBallast) obtained during the in water test ballast.  
- It also takes into account the min/max software limits and VBD max volume.  
- The parallel grey lines correspond to different ballasts (the -100,+100,+200, etc. lines are the operation regions for different CVBD >> -100 means CVBD-100) in the same water (same sigmaBallast, different CVBD). This is, the operating ranges based on variations in the ballast (adding/removing lead/foam) for the same glider. 


Online script: https://colab.research.google.com/drive/1uQvEEK3j1_7uMVuugx-v0tVB7ibRWKST?usp=sharing
