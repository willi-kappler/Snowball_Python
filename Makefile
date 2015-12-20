clean:
	find ./ -iname "*~" -exec rm -fv {} \;
	find ./ -iname "*.pyc" -exec rm -fv {} \;
