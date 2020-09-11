#!/usr/bin/awk
# Note: Averages are calculated, but perhaps the median would give a better indication

BEGIN { FS=","; min_enroll=3000; max_enroll=0;}

/^[^#]/ { graduate[$1,$3]++; 
	enroll_year_count[$1]++;
	min_enroll = ($1<min_enroll) ? $1 : min_enroll;
	max_enroll = ($1>max_enroll) ? $1 : max_enroll;
}

END { print("Statistics for graduates from " min_enroll " to " max_enroll);
	total_sum = 0;
	total_count = 0;
	for (i=min_enroll; i<=max_enroll; i++) {
		year_sum = 0;
		total_count += enroll_year_count[i];
		if (enroll_year_count[i]>0) {
			for (j=0; j<20; j++)
			{
				year_sum += graduate[i,j]*j;
				total_sum += graduate[i,j]*j;
			}
			print("Average time to graduate for the cohort of " i ": " year_sum/enroll_year_count[i] " years.");
		}
	}
	print("Average time to graduate for all students: " total_sum/total_count " years.");
}

