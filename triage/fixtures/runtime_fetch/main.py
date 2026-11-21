from nilearn import datasets

haxby = datasets.fetch_haxby(subjects=[1])
print(haxby.func[0])
