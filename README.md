# 5278-web-crawler

## Instruction

Download videos of posts on [5278](http://www.5278.cc/forum.php?gid=22).

## Usage

-   Install [Chrome](https://www.google.com/chrome/?brand=CHBD&gclid=Cj0KCQjwl8XtBRDAARIsAKfwtxD53tG_IZsUcMuwakYR968gH06p6R_lylXat2cj_Z1_JzBYpBcHFOAaAideEALw_wcB&gclsrc=aw.ds) on your computer.

-   Download [Chromedriver](https://chromedriver.chromium.org/downloads) first. Unzip it and put `chromedriver.exe` in folder `/bin`. 

-   Copy `secret.py.dist` as `secret.py` in the same folder.

```
python main.py *bookmark_path*
    
Args:
    *bookmark_path*: Bookmark input path (a file including one URL per line).
```

## Requirements

-   `python3`.
-   `selenium`.
-    Details are omitted.

## License

MIT License.
