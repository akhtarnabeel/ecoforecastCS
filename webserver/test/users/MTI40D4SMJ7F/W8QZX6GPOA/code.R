retJSON <- paste(
      "{\"body\": {
        \"xlab\": \"Time\",\n \"ylab\": \"Mean GCC\"}
        }"
      )
write(retJSON, file="out.json")