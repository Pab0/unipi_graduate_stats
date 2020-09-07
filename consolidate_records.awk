#!/usr/bin/awk

BEGIN { FS=",";
	print "# ID, Surname, Name, Father's name, Enrollment Year, Graduation Year, Years Studied"}

NR==FNR { seen[$1] = 1 }

NR>FNR {
	if (!seen[$1]) {
		seen[$1] = 1;
		surname[$1] = $2;
		name[$1] = $3;
		fathers_name[$1] = $4;

		split(FILENAME,fname,".");
		graduation_year[$1] = fname[1];

		enrol = substr($1,2,2);
		enrol_year[$1] = enrol>80 ? "19" enrol : "20" enrol;
		study_years[$1] = graduation_year[$1] - enrol_year[$1];
	}
}


END { for (key in graduation_year) {
		print key "," surname[key] "," name[key] "," fathers_name[key] "," enrol_year[key] "," graduation_year[key] "," study_years[key]
	}
}
